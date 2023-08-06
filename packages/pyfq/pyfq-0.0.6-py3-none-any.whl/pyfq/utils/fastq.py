import sys
import gzip
from itertools import islice


class Fastq():

    '''Yields read records from fastq files.'''

    def __init__(self, fastq_file):
        self.fastq_file = fastq_file

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def __str__(self):
        return '{} object for {}'.format(self.__class__.__name__, self.fastq_file)

    def __repr__(self):
        return '{} object for {}'.format(self.__class__.__name__, self.fastq_file)

    def __len__(self):
        '''Returns number of reads'''
        return len(self)

    def __iter__(self):
        if self.fastq_file.endswith(('.fastq.gz', 'fq.gz')):
            with gzip.open(self.fastq_file, 'rb') as f:
                while True:
                    read_record = [line.decode('utf-8').strip()
                                   for line in islice(f, 4)]
                    if not read_record:
                        break
                    yield read_record[0], read_record[1], read_record[3]
            f.close()

        elif self.fastq_file.endswith(('.fastq', '.fq')):
            while True:
                read_record = [line.strip() for line in islice(f, 4)]
                if not read_record:
                    break
                yield read_record[0], read_record[1], read_record[3]
            f.close()
        else:
            sys.stderr.write('Are you sure this is a fastq file??\n')
            sys.exit()

    def to_fastq(self, fastq_file):
        with open(fastq_file, 'w') as f:
            for read_record in self:
                f.write('{}\n{}\n+\n{}\n'.format(
                    read_record[0], read_record[1], read_record[2]))

    def to_fasta(self, fasta_file):
        with open(fasta_file, 'w') as f:
            for read_record in self:
                f.write('>{}\n{}\n'.format(
                    read_record[0].strip('@'), read_record[1]))
            f.close()
