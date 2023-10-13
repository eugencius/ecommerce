import re


class ValidatingCPF:
    def format_cpf(self, cpf):
        return re.sub(r"[^0-9]", "", cpf)[:-2]

    def zipped_list(self, cpf_formatted, reversed=True):
        list_cpf = [int(i) for i in cpf_formatted]
        list_range = [n for n in range(2, 11)]

        if reversed:
            list_range.reverse()

        return list(zip(list_cpf, list_range))

    def modulus_calc(self, list_cpf):
        count = sum([n * i for n, i in list_cpf])
        return (count * 10) % 11

    def calculate_first_digit(self, cpf):
        cpf_formated = self.format_cpf(cpf)

        list_cpf = self.zipped_list(cpf_formated)
        calc = self.modulus_calc(list_cpf)

        return 0 if calc > 9 else calc

    def calculate_second_digit(self, cpf):
        cpf_formated = self.format_cpf(cpf)

        list_cpf = self.zipped_list(cpf_formated, reversed=False)

        calc = self.modulus_calc(list_cpf)

        return 0 if calc > 9 else calc

    def validate_cpf(self, cpf):
        if bool(re.match(r"^(.)\1*$", cpf)):
            return False

        first_digit = self.calculate_first_digit(cpf)
        second_digit = self.calculate_second_digit(cpf)

        new_cpf = f"{self.format_cpf(cpf)}{first_digit}{second_digit}"
        formatted_cpf = re.sub(r"[^0-9]", "", cpf)

        return True if formatted_cpf == new_cpf else False
