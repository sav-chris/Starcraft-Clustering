import sys
import os

TEST_DATA_DIR: str = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'test.data'))
TEST_REPLAY_HAS: str = '20220223 - GAME 1 - Has vs Cyan - P vs P - Hardwire LE.SC2Replay'
TEST_LEVENSHTEIN_DIR: str = os.path.join(TEST_DATA_DIR, 'levenshtein')
TEST_BUILD_ORDER_DIR: str = os.path.join(TEST_DATA_DIR, 'build.order')
TEST_BUILD_ORDER_EXAMPLE_DIR: str = os.path.join(TEST_DATA_DIR, 'build.order.example')
TEST_LABEL_ENCODER_DIR: str = os.path.join(TEST_DATA_DIR, 'label.encoder')


