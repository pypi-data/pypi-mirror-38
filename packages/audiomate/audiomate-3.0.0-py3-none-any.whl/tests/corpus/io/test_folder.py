from audiomate.corpus import io

from tests import resources


class TestFolderReader:

    def test_load(self):
        path = resources.sample_corpus_path('folder')
        reader = io.FolderReader()

        ds = reader.load(path)

        assert ds.num_tracks == 7
        assert ds.num_utterances == 7
        assert ds.num_issuers == 0

        assert set(ds.tracks.keys()) == {
            'empty',
            'wav_1',
            'wav_2',
            'wav_3',
            'wav_4',
            'wav_200_samples',
            'wav_invalid'
        }
        assert set(ds.utterances.keys()) == {
            'empty',
            'wav_1',
            'wav_2',
            'wav_3',
            'wav_4',
            'wav_200_samples',
            'wav_invalid'
        }
