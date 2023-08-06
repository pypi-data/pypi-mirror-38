import os

import pytest

from audiomate import corpus
from audiomate.corpus import io
from tests import resources


@pytest.fixture
def reader():
    return io.AEDReader()


@pytest.fixture
def data_path():
    return resources.sample_corpus_path('aed')


class TestAEDReader:

    def test_load_tracks(self, reader, data_path):
        ds = reader.load(data_path)

        test_path = os.path.join(data_path, 'test')
        train_path = os.path.join(data_path, 'train')

        assert ds.num_tracks == 10

        assert ds.tracks['acoustic_guitar_16'].idx == 'acoustic_guitar_16'
        assert ds.tracks['acoustic_guitar_16'].path == os.path.join(test_path, 'acoustic_guitar_16.wav')

        assert ds.tracks['footstep_300'].idx == 'footstep_300'
        assert ds.tracks['footstep_300'].path == os.path.join(test_path, 'footstep_300.wav')

        assert ds.tracks['violin_36'].idx == 'violin_36'
        assert ds.tracks['violin_36'].path == os.path.join(test_path, 'violin_36.wav')

        assert ds.tracks['airplane_1'].idx == 'airplane_1'
        assert ds.tracks['airplane_1'].path == os.path.join(train_path, 'airplane', 'airplane_1.wav')

        assert ds.tracks['airplane_23'].idx == 'airplane_23'
        assert ds.tracks['airplane_23'].path == os.path.join(train_path, 'airplane', 'airplane_23.wav')

        assert ds.tracks['airplane_33'].idx == 'airplane_33'
        assert ds.tracks['airplane_33'].path == os.path.join(train_path, 'airplane', 'airplane_33.wav')

        assert ds.tracks['footstep_16'].idx == 'footstep_16'
        assert ds.tracks['footstep_16'].path == os.path.join(train_path, 'footstep', 'footstep_16.wav')

        assert ds.tracks['helicopter_9'].idx == 'helicopter_9'
        assert ds.tracks['helicopter_9'].path == os.path.join(train_path, 'helicopter', 'helicopter_9.wav')

        assert ds.tracks['tone_12'].idx == 'tone_12'
        assert ds.tracks['tone_12'].path == os.path.join(train_path, 'tone', 'tone_12.wav')

        assert ds.tracks['tone_35'].idx == 'tone_35'
        assert ds.tracks['tone_35'].path == os.path.join(train_path, 'tone', 'tone_35.wav')

    def test_load_utterances(self, reader, data_path):
        ds = reader.load(data_path)

        assert ds.num_utterances == 10

        assert ds.utterances['acoustic_guitar_16'].idx == 'acoustic_guitar_16'
        assert ds.utterances['acoustic_guitar_16'].track.idx == 'acoustic_guitar_16'
        assert ds.utterances['acoustic_guitar_16'].issuer is None
        assert ds.utterances['acoustic_guitar_16'].start == 0
        assert ds.utterances['acoustic_guitar_16'].end == -1

        assert ds.utterances['airplane_23'].idx == 'airplane_23'
        assert ds.utterances['airplane_23'].track.idx == 'airplane_23'
        assert ds.utterances['airplane_23'].issuer is None
        assert ds.utterances['airplane_23'].start == 0
        assert ds.utterances['airplane_23'].end == -1

        assert ds.utterances['tone_12'].idx == 'tone_12'
        assert ds.utterances['tone_12'].track.idx == 'tone_12'
        assert ds.utterances['tone_12'].issuer is None
        assert ds.utterances['tone_12'].start == 0
        assert ds.utterances['tone_12'].end == -1

    def test_load_issuers(self, reader, data_path):
        ds = reader.load(data_path)

        assert ds.num_issuers == 0

    def test_load_labels(self, reader, data_path):
        ds = reader.load(data_path)

        utt = ds.utterances['airplane_23']
        assert len(utt.label_lists) == 1
        assert utt.label_lists[corpus.LL_SOUND_CLASS][0].value == 'airplane'
        assert utt.label_lists[corpus.LL_SOUND_CLASS][0].start == 0
        assert utt.label_lists[corpus.LL_SOUND_CLASS][0].end == -1

        utt = ds.utterances['tone_12']
        assert len(utt.label_lists) == 1
        assert utt.label_lists[corpus.LL_SOUND_CLASS][0].value == 'tone'
        assert utt.label_lists[corpus.LL_SOUND_CLASS][0].start == 0
        assert utt.label_lists[corpus.LL_SOUND_CLASS][0].end == -1

        utt = ds.utterances['acoustic_guitar_16']
        assert len(utt.label_lists) == 1
        assert utt.label_lists[corpus.LL_SOUND_CLASS][0].value == 'acoustic_guitar'
        assert utt.label_lists[corpus.LL_SOUND_CLASS][0].start == 0
        assert utt.label_lists[corpus.LL_SOUND_CLASS][0].end == -1

    def test_load_fold_subsets(self, reader, data_path):
        ds = reader.load(data_path)

        assert len(ds.subviews) == 2

        assert ds.subviews['train'].num_utterances == 7
        assert ds.subviews['test'].num_utterances == 3
