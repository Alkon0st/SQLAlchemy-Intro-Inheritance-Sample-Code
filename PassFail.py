from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from Enrollment import Enrollment


class PassFail(Enrollment):
    __tablename__ = "pass_fail"
    # I HAD put Integer after the table name, but apparently it picks that up from the parent PK.
    passFailId: Mapped[int] = mapped_column('pass_fail_id',
                                            ForeignKey("enrollments.enrollment_id",
                                                       ondelete="CASCADE"), primary_key=True)
    applicationDate: Mapped[Date] = mapped_column('application_date', Date, nullable=False)
    __mapper_args__ = {"polymorphic_identity": "pass_fail"}

    def __init__(self, section, student, application_date: Date):
        super().__init__(section, student)
        self.applicationDate = application_date

    def __str__(self):
        return f"PassFail Enrollment: {super().__str__()}"
