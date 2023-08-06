import unittest
from has import *

reference_records = { # Records which correspond to the data files in folder dataset
    '34dc214a2aea8d7c254a9d6dc351e0d3c0088ad998eed6053b78877785fcdff1': 'triangle/triangle0.png',
    '566f5fa0703f5c2877c38fb3aae0fabbc5f9cdb25499b4f03ca75a6eb3827961': 'square/square0.png',
    '67240c2cee6e9c77df1192890b1cf4deb265a5a6afdb4a5ecc03e93cc5889cef': 'triangle/triangle2.png',
    'dfb6352f5d42793b58ac74f2cacf5f1f82bdb1470a30941224a0f1e34766aeb4': 'square/square2.png',
    'e361db7913f495dafee06657ea67043a49c06fa1a3c57d3ed5b1a9048455de8f': 'square/square1.png',
    'f7994454bf5a880c5741b3af8e0ababf77f8c450fe47ed8b5c6f7b9d38c9115f': 'triangle/triangle1.png',
}

class TestHasMethods(unittest.TestCase):
    ''' Set of unit tests for has.py '''
    def test_read_file_records(self):
        ''' Test the function to read in file records '''
        file_records = read_file_records('snapshot.has')
        self.compare_records(file_records, reference_records)


    def test_gen_file_records(self):
        ''' Test the function to generate file records '''
        file_records = {k:v for k,v in gen_file_records('dataset')}
        self.compare_records(file_records, reference_records)


    def compare_records(self, file_records, reference_records):
        ''' Compare file_records and reference_records to make sure they are identical '''
        # Find hashes in reference_records not in file_records
        for file_hash in (set(reference_records) - set(file_records)):
            filename = reference_records[file_hash]
            self.fail('Not found in file_records %s:%s' % (file_hash, filename))

        # Find hashes in file_records not in reference_records
        for file_hash in (set(file_records) - set(reference_records)):
            filename = file_records[file_hash]
            self.fail('Not found in reference_records %s:%s' % (file_hash, filename))

        # Make sure all of the filenames are the same
        for file_hash in set(file_records).intersection(reference_records):
            stored_fn = file_records[file_hash] # Stored filename
            ref_fn = reference_records[file_hash] # Reference filename
            error_msg = 'Reference filename %s did not match stored filename %s' % (ref_fn, stored_fn)
            self.assertEqual(ref_fn, stored_fn, error_msg)


if __name__ == '__main__':
    unittest.main()
