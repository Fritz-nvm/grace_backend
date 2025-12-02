class TestimonialNotFoundError(Exception):
    """Raised when a testimonial is not found"""

    pass


class TestimonialAlreadyExistsError(Exception):
    """Raised when a testimonial with same client name already exists"""

    pass


class TestimonialValidationError(Exception):
    """Raised when testimonial data validation fails"""

    pass
