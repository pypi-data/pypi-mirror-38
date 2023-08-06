from unittest import TestCase
from vcr import VCR
import os
import shutil
import click
from click.testing import CliRunner
import mock
from icloudpd.base import main
from tests.helpers.print_result_exception import print_result_exception

vcr = VCR(decode_compressed_response=True)

class ListingRecentPhotosTestCase(TestCase):
    def test_listing_recent_photos(self):
        if os.path.exists("tests/fixtures/Photos"):
            shutil.rmtree("tests/fixtures/Photos")
        os.makedirs("tests/fixtures/Photos")

        # Note - This test uses the same cassette as test_download_photos.py
        with vcr.use_cassette("tests/vcr_cassettes/listing_photos.yml"):
            # Pass fixed client ID via environment variable
            os.environ["CLIENT_ID"] = "DE309E26-942E-11E8-92F5-14109FE0B321"
            runner = CliRunner()
            result = runner.invoke(
                main,
                [
                    "--username",
                    "jdoe@gmail.com",
                    "--password",
                    "password1",
                    "--recent",
                    "5",
                    "--only-print-filenames",
                    "--no-progress-bar",
                    "tests/fixtures/Photos",
                ],
            )
            print_result_exception(result)
            filenames = result.output.splitlines()

            self.assertEqual(len(filenames), 8)
            self.assertEqual(
                "tests/fixtures/Photos/2018/07/31/IMG_7409.JPG", filenames[0]
            )
            self.assertEqual(
                "tests/fixtures/Photos/2018/07/31/IMG_7409.MOV", filenames[1]
            )
            self.assertEqual(
                "tests/fixtures/Photos/2018/07/30/IMG_7408.JPG", filenames[2]
            )
            self.assertEqual(
                "tests/fixtures/Photos/2018/07/30/IMG_7408.MOV", filenames[3]
            )
            self.assertEqual(
                "tests/fixtures/Photos/2018/07/30/IMG_7407.JPG", filenames[4]
            )
            self.assertEqual(
                "tests/fixtures/Photos/2018/07/30/IMG_7407.MOV", filenames[5]
            )
            self.assertEqual(
                "tests/fixtures/Photos/2018/07/30/IMG_7405.MOV", filenames[6]
            )
            self.assertEqual(
                "tests/fixtures/Photos/2018/07/30/IMG_7404.MOV", filenames[7]
            )


            assert result.exit_code == 0

    def test_listing_recent_photos_with_missing_filenameEnc(self):
        if os.path.exists("tests/fixtures/Photos"):
            shutil.rmtree("tests/fixtures/Photos")
        os.makedirs("tests/fixtures/Photos")

        # Note - This test uses the same cassette as test_download_photos.py
        with vcr.use_cassette("tests/vcr_cassettes/listing_photos_missing_filenameEnc.yml"):
            with mock.patch("icloudpd.base.open", create=True) as mock_open:
                # Pass fixed client ID via environment variable
                os.environ["CLIENT_ID"] = "DE309E26-942E-11E8-92F5-14109FE0B321"
                runner = CliRunner()
                result = runner.invoke(
                    main,
                    [
                        "--username",
                        "jdoe@gmail.com",
                        "--password",
                        "password1",
                        "--recent",
                        "1",
                        "--only-print-filenames",
                        "--no-progress-bar",
                        "tests/fixtures/Photos",
                    ],
                )
                print_result_exception(result)

                self.assertEqual.__self__.maxDiff = None
                self.assertEqual("""\
KeyError: 'filenameEnc' attribute was not found in the photo fields!
icloudpd has saved the photo record to: ./icloudpd-photo-error.json
Please create a Gist with the contents of this file: https://gist.github.com
Then create an issue on GitHub: https://github.com/ndbroadbent/icloud_photos_downloader/issues
Include a link to the Gist in your issue, so that we can see what went wrong.

""" , result.output
                )
                mock_open.assert_called_once_with('icloudpd-photo-error.json', 'w')

                assert result.exit_code == 0
