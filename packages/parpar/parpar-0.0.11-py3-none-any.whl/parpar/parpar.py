import os, itertools, shutil
from multiprocessing import Value, Pool, Lock, current_process
from sil import Sil
from .utils import (
    filelines, linesplit, linemend,
    superdirs, readlines_split, dir_from_cols,
    sharddir, shardname, shardloc
)

default_sil_options = {
    'length': 40,
    'every': 1
}

class ParPar:
    def __init__(self):
        pass

    def shard(self,
        input_file,
        output_dir,
        columns,
        delim='\t',
        newline='\n',
        sil_opts = default_sil_options
    ):
        '''
        Given the input_file and the columns, reads each line of the input_file as
        dumps the content into file the directory:

            output_dir/<columns[0]>/.../<columns[N]>/basename(<input_file>)

        where <columns[i]> is the value found in the current line at position i
        after being split by the specified delim.

        Args:
            input_file (str): full path to the file.
            output_dir (str): full path to a directory in which to dump. WARNING:
                everything in specified directory will be PERMANENTLY REMOVED.
            columns (list): the columns across which to shard. The values found in
                these columns will be used as directory names (nested).
        Kwargs:
            delim (str): Defaults to '\t'
            newline (str): Defaults to '\n'
            sil_opts (dict): Defaults to {'length': 40, 'every': 1}. See Sil package.

        Returns:
            None
        '''
        lno = filelines(input_file)
        sts = Sil(lno, **sil_opts)
        basename = os.path.basename(input_file)
        files_made = set({})

        file_objs = {}

        if os.path.isdir(output_dir):
            shutil.rmtree(output_dir)

        with open(input_file, 'r') as f:
            for line in f:
                fields = linesplit(line, delim, newline)
                dest = dir_from_cols(fields, columns)
                files_made.add(dest)
                dir_path = os.path.join(output_dir, dest)
                if not os.path.isdir(dir_path):
                    os.makedirs(dir_path)
                    file_objs[dir_path] = open(os.path.join(dir_path, basename), 'a')

                o = file_objs[dir_path]
                o.write(linemend(fields, delim, newline))
                suffix = '\t{} files made'.format(len(files_made))
                # f'\t{len(files_made)} files made'
                sts.tick(suffix=suffix)

        for fo in file_objs.values():
            fo.close()

    def shard_files(self, directory):
        '''
        Args:
            directory (str): The topmost directory of a shared file.

        Returns:
            (list): The list of all files under directory (regardless of depth).
        '''
        file_paths = []
        for path, subdirs, files in os.walk(directory):
            if not files: continue
            file_paths += [os.path.join(path, f) for f in files]
        return file_paths

    def shard_walk(self, directory):
        '''
        Args:
            directory (str): The topmost directory of a shared file.

        Returns:
            (dict): A nested dictionary containing the folder names found at
                each level. The bottomost level of the dictionary contains files
                found.

                e.g.  if in directory there was directory/key_1/key_2/file_1
                {
                    key_1: {
                        key: 2: [ file_1, ...]
                    }

                }
        '''
        walk = {}
        for path, subdirs, files in os.walk(directory):
            supdirs = superdirs(path, directory)
            drilldown = walk

            for i, key in enumerate(supdirs):
                if key not in drilldown:
                    leaf_q = (files and i == len(supdirs) - 1)
                    drilldown[key] = [] if leaf_q else {}

                drilldown = drilldown[key]

            if files:
                drilldown += files

        return walk

    def shard_keys(self, directory):
        '''
        Args:
            directory (str): The topmost directory of a shared file.

        Returns:
            (list): A list of lists for the directory names found at each level
                after under directory
                e.g.

                directory
                    key_1
                        key_a
                        key_b
                    key_2
                        ...
                returns
                [ [key_1, key_2, ...], [key_a, key_b, ...], ... ]
        '''
        level_keys = []
        for path, subdirs, files in os.walk(directory):
            supdirs = superdirs(path, directory)
            if len(level_keys) > len(supdirs):
                level_keys[len(supdirs)] += subdirs
            else:
                level_keys.append(subdirs)
        return [list(set(keys)) for keys in level_keys]

    def sharded_records(self, files=None, directory=None):
        '''
        Args:
            directory (str): The topmost directory of a shared file.

        Returns:
            (int): Total number of lines in all leaf files under directory.
        '''
        if files is None and directory is not None: files = self.shard_files(directory)

        return sum([filelines(f) for f in files])


    def assemble_shard(self, directory, delim='\t', newline='\n'):
        '''
        Args:
            directory (str): The topmost directory of a shared file.

        Kwargs:
            delim (str): Defaults to '\t'
            newline (str): Defaults to '\n'

        Returns:
            (list): The list of lists, where each sub-list is a record found
                in one of the sharded leaf files after being split by delim.
                (i.e. all records are returned together)
        '''
        results = []
        files = self.shard_files(directory)


        with Pool(processes=os.cpu_count()) as pool:
            sarg = [(f, delim, newline) for f in files]
            lines = pool.starmap(readlines_split, sarg)

        return list(itertools.chain.from_iterable(lines))



    _shared_current = Value('i', 0)
    _shared_lock = Lock()

    def shard_line_apply(self,
        directory,
        function,
        args=[],
        kwargs={},
        processes=None,
        sil_opts=default_sil_options
    ):
        '''
        Args:
            directory (str): The topmost directory of a shared file.
            function (func): The function which will be parallelized. This function
                MUST be defined so that it can be called as:

                    func(line, *args, **kwargs)



        Kwargs:
            args (list): arguments to be passed to <function> on each thread.
            kwargs (dict): key-word arguments to be passed to <function> on each thread.
                Three key-words are RESERVED.
                    1. lock:          a lock, if needed, to prevent race conditions.
                    2. full_path:     the full path to the file which was opened.
                    3. relative_path: the path under (directory) to the file which
                                      was opened.

            processes (int): Defaults to ALL availble on the calling computer.
                The number of threads to spawn.

            sil_opts (dict): Defaults to {'length': 40, 'every': 1}. See Sil package.

            delim (str): Defaults to '\t'
            newline (str): Defaults to '\n'

        Returns:
            None
        '''
        if processes is None: processess = os.cpu_count()
        sfiles = self.shard_files(directory)
        records = self.sharded_records(sfiles)
        sts = Sil(records, **sil_opts)

        with Pool(processes=processess) as pool:
            self._shared_current.value = -1

            sargs = [
                (directory, file, sts, function, args, kwargs) for file in sfiles
            ]
            pool.starmap(self._shard_line_apply, sargs)

            pool.close()
            pool.join()
            pool.terminate()


    def _shard_line_apply(self,
        directory,
        file,
        status,
        function,
        args,
        kwargs
    ):
        kwargs['lock']            = self._shared_lock
        kwargs['shared_current']  = self._shared_current
        kwargs['status']          = status
        kwargs['full_path']       = file
        kwargs['shard_name']      = shardname(file, directory)
        kwargs['shard_dir']       = sharddir(file, directory)
        kwargs['shard_loc']       = shardloc(file, directory)
        kwargs['relative_path']   = os.path.join(*superdirs(file, directory))
        kwargs['current_process'] = current_process().name


        cp = kwargs['current_process']

        os_name = kwargs['output_shard_name'] if 'output_shard_name' in kwargs else None
        os_loc  = kwargs['output_shard_loc']  if 'output_shard_loc'  in kwargs else kwargs['shard_loc']

        if os_name is not None:
            dest = os.path.join(os_loc, os_name, os.path.dirname(kwargs['relative_path']))
            kwargs['dest'] = dest
            self._shared_lock.acquire()
            try:
                if os.path.isdir(dest):
                    shutil.rmtree(dest)
                os.makedirs(dest)
            finally:
                self._shared_lock.release()


        with open(file, 'r') as f:
            for line in f:
                function(line, *args, **kwargs)
                self._shared_lock.acquire()
                try:
                    self._shared_current.value += 1
                    suffix = '\tprocess: {}'.format(cp)
                    # f'\tprocess: {cp}'
                    status.update(current=self._shared_current.value, suffix=suffix)
                finally:
                    self._shared_lock.release()


    def shard_file_apply(self,
        directory,
        function,
        args=[],
        kwargs={},
        processes=None,
        sil_opts=default_sil_options
    ):
        '''
        Args:
            directory (str): The topmost directory of a shared file.
            function (func): The function which will be parallelized. This function
                MUST be defined so that it can be called as:

                    func(line, *args, **kwargs)



        Kwargs:
            args (list): arguments to be passed to <function> on each thread.
            kwargs (dict): key-word arguments to be passed to <function> on each thread.
                Three key-words are RESERVED.
                    1. lock:          a lock, if needed, to prevent race conditions.
                    2. full_path:     the full path to the file which was opened.
                    3. relative_path: the path under (directory) to the file which
                                      was opened.

            processes (int): Defaults to ALL availble on the calling computer.
                The number of threads to spawn.

            sil_opts (dict): Defaults to {'length': 40, 'every': 1}. See Sil package.

            delim (str): Defaults to '\t'
            newline (str): Defaults to '\n'

        Returns:
            None
        '''
        if processes is None: processess = os.cpu_count()
        sfiles = self.shard_files(directory)
        records = self.sharded_records(sfiles)
        sts = Sil(records, **sil_opts)

        with Pool(processes=processess) as pool:
            self._shared_current.value = -1

            sargs = [
                (directory, file, sts, function, args, kwargs) for file in sfiles
            ]
            pool.starmap(self._shard_file_apply, sargs)

            pool.close()
            pool.join()
            pool.terminate()


    def _shard_file_apply(self,
        directory,
        file,
        status,
        function,
        args,
        kwargs
    ):
        kwargs['lock']            = self._shared_lock
        kwargs['shared_current']  = self._shared_current
        kwargs['status']          = status
        kwargs['full_path']       = file
        kwargs['shard_name']      = shardname(file, directory)
        kwargs['shard_dir']       = sharddir(file, directory)
        kwargs['shard_loc']       = shardloc(file, directory)
        kwargs['relative_path']   = os.path.join(*superdirs(file, directory))
        kwargs['current_process'] = current_process().name


        os_name = kwargs['output_shard_name'] if 'output_shard_name' in kwargs else None
        os_loc = kwargs['output_shard_loc'] if 'output_shard_loc' in kwargs else kwargs['shard_loc']

        if os_name is not None:
            dest = os.path.join(os_loc, os_name, os.path.dirname(kwargs['relative_path']))
            kwargs['dest'] = dest
            self._shared_lock.acquire()
            try:
                if os.path.isdir(dest):
                    shutil.rmtree(dest)
                os.makedirs(dest)
            finally:
                self._shared_lock.release()


        function(file, *args, **kwargs)
