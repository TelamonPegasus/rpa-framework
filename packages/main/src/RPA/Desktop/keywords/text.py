import time
from typing import Optional

from RPA.core.geometry import Region
from RPA.Desktop.keywords import LibraryContext, keyword, screen, HAS_RECOGNITION

if HAS_RECOGNITION:
    from RPA.recognition import ocr


def ensure_recognition():
    if not HAS_RECOGNITION:
        raise ValueError(
            "Keyword requires OCR features, please install the "
            "rpaframework-recognition package"
        )


class TextKeywords(LibraryContext):
    """Keywords for reading screen information and content."""

    @keyword
    def read_text(self, locator: Optional[str] = None):
        """Read text using OCR from the screen, or an area of the
        screen defined by the given locator.

        :param locator: Location of element to read text from
        """
        ensure_recognition()

        if locator is not None:
            element = self.ctx.wait_for_element(locator)
            if not isinstance(element, Region):
                raise ValueError("Locator must resolve to a region")

            self.logger.info("Reading text from element: %s", element)
            image = screen.grab(element)
        else:
            self.logger.info("Reading text from screen")
            image = screen.grab()

        screen.log_image(image)

        start_time = time.time()
        text = ocr.read(image)
        self.logger.info("Read text in %.2f seconds", time.time() - start_time)

        return text
