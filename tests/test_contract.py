import importlib.util,unittest,tempfile,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('remake',ROOT/'scripts/remake.py');remake=importlib.util.module_from_spec(spec);spec.loader.exec_module(remake)

class ContractTests(unittest.TestCase):
    def test_inclusive_coverage(self):
        remake.validate_coverage([{'id':'a','f0':0,'f1':2},{'id':'b','f0':3,'f1':5}],6)
    def test_gap_overlap_duplicate_and_short_end_rejected(self):
        for shots in [[{'id':'a','f0':1,'f1':5}],[{'id':'a','f0':0,'f1':3},{'id':'b','f0':3,'f1':5}],[{'id':'a','f0':0,'f1':2},{'id':'a','f0':3,'f1':5}],[{'id':'a','f0':0,'f1':4}]]:
            with self.assertRaises(ValueError):remake.validate_coverage(shots,6)
    def test_scaffold_arbitrary_path_and_overwrite_protection(self):
        with tempfile.TemporaryDirectory(prefix='remake test ') as t:
            film=Path(t)/'film with spaces';c={'width':320,'height':180,'fps':'30000/1001','frame_count':6,'duration':.2002,'pad':4,'brand':{'name':'Marca'}}
            remake.scaffold(film,c)
            self.assertTrue((film/'assets/core.js').is_file());self.assertIn('29.970', (film/'film-settings.js').read_text())
            self.assertNotIn('../engine',(film/'page.html').read_text())
            with self.assertRaises(ValueError):remake.scaffold(film,c)

if __name__=='__main__':unittest.main()
