from typing import Any



class ELDLogService:
    """
    FMCSA Hours of Service (HOS) calculation service.

    Handles:

    - Daily driving limits
    - 14-hour duty window
    - 60/70 hour cycle limits
    - 30-minute break requirement
    - 34-hour restart calculation
    - Adverse driving conditions
    - HOS violation detection
    """

    MAX_DRIVING_HOURS = 11

    MAX_ON_DUTY_WINDOW = 14

    BREAK_AFTER_DRIVING = 8

    BREAK_DURATION_MINUTES = 30

    CYCLE_LIMIT_60 = 60

    CYCLE_LIMIT_70 = 70

    RESTART_HOURS = 34

    ADVERSE_DRIVING_EXTENSION = 2



    def generate_daily_summary(
        self,
        driving_hours: float,
        on_duty_hours: float,
        cycle_hours_used: float,
        cycle_type: str = "70",
        adverse_conditions: bool = False,
    ) -> dict[str, Any]:
        """
        Generate complete FMCSA HOS summary.
        """


        driving_limit = self.get_driving_limit(
            adverse_conditions
        )


        duty_limit = self.get_duty_limit(
            adverse_conditions
        )


        return {

            "driving_hours": driving_hours,

            "on_duty_hours": on_duty_hours,

            "cycle_hours_used": cycle_hours_used,


            "remaining_driving_hours":
                self.calculate_remaining(
                    driving_limit,
                    driving_hours
                ),


            "remaining_on_duty_hours":
                self.calculate_remaining(
                    duty_limit,
                    on_duty_hours
                ),


            "remaining_cycle_hours":
                self.remaining_cycle_hours(
                    cycle_hours_used,
                    cycle_type
                ),


            "break_required":
                self.break_required(
                    driving_hours
                ),


            "off_duty_reset_required":
                self.off_duty_reset_required(
                    cycle_hours_used,
                    cycle_type
                ),


            "hos_violations":
                self.detect_violations(
                    driving_hours,
                    on_duty_hours,
                    cycle_hours_used,
                    cycle_type,
                    adverse_conditions,
                ),
        }



    def get_driving_limit(
        self,
        adverse_conditions: bool
    ) -> float:
        """
        Return legal driving limit.
        """

        limit = self.MAX_DRIVING_HOURS


        if adverse_conditions:
            limit += self.ADVERSE_DRIVING_EXTENSION


        return limit



    def get_duty_limit(
        self,
        adverse_conditions: bool
    ) -> float:
        """
        Return legal duty window.
        """

        limit = self.MAX_ON_DUTY_WINDOW


        if adverse_conditions:
            limit += self.ADVERSE_DRIVING_EXTENSION


        return limit



    def calculate_remaining(
        self,
        limit: float,
        used: float
    ) -> float:
        """
        Calculate remaining hours.
        """

        return max(
            round(limit - used, 2),
            0
        )



    def remaining_cycle_hours(
        self,
        cycle_hours_used: float,
        cycle_type: str,
    ) -> float:
        """
        Calculate remaining cycle hours.
        """


        limit = (
            self.CYCLE_LIMIT_60
            if cycle_type == "60"
            else self.CYCLE_LIMIT_70
        )


        return max(
            round(limit - cycle_hours_used, 2),
            0
        )



    def break_required(
        self,
        driving_hours: float
    ) -> bool:
        """
        FMCSA:
        30-minute break required
        after 8 cumulative driving hours.
        """

        return driving_hours >= self.BREAK_AFTER_DRIVING



    def off_duty_reset_required(
        self,
        cycle_hours_used: float,
        cycle_type: str
    ) -> bool:
        """
        Check if driver has exhausted cycle hours
        and requires restart.
        """


        limit = (
            self.CYCLE_LIMIT_60
            if cycle_type == "60"
            else self.CYCLE_LIMIT_70
        )


        return cycle_hours_used >= limit



    def restart_available(
        self,
        off_duty_hours: float
    ) -> bool:
        """
        Check 34-hour restart eligibility.
        """

        return off_duty_hours >= self.RESTART_HOURS



    def detect_violations(
        self,
        driving_hours: float,
        on_duty_hours: float,
        cycle_hours_used: float,
        cycle_type: str,
        adverse_conditions: bool = False,
    ) -> list[str]:
        """
        Detect FMCSA violations.
        """


        violations = []


        driving_limit = self.get_driving_limit(
            adverse_conditions
        )


        duty_limit = self.get_duty_limit(
            adverse_conditions
        )


        if driving_hours > driving_limit:

            violations.append(
                f"Driving limit exceeded. "
                f"Maximum allowed: {driving_limit} hours."
            )


        if on_duty_hours > duty_limit:

            violations.append(
                f"14-hour duty window exceeded. "
                f"Maximum allowed: {duty_limit} hours."
            )



        cycle_limit = (
            self.CYCLE_LIMIT_60
            if cycle_type == "60"
            else self.CYCLE_LIMIT_70
        )


        if cycle_hours_used > cycle_limit:

            violations.append(
                f"{cycle_limit}-hour cycle limit exceeded."
            )


        if self.break_required(driving_hours):

            violations.append(
                "30-minute break required after 8 hours driving."
            )


        return violations



    def calculate_available_driving_time(
        self,
        driving_hours: float,
        adverse_conditions: bool = False,
    ) -> float:
        """
        Calculate remaining driving time.
        """


        return self.calculate_remaining(
            self.get_driving_limit(
                adverse_conditions
            ),
            driving_hours
        )



    def calculate_available_on_duty_time(
        self,
        on_duty_hours: float,
        adverse_conditions: bool = False,
    ) -> float:
        """
        Calculate remaining duty window.
        """


        return self.calculate_remaining(
            self.get_duty_limit(
                adverse_conditions
            ),
            on_duty_hours
        )