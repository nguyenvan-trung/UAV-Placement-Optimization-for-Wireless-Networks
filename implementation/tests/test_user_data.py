import unittest

import pandas as pd

from src.input.data_validator import validate_users
from src.preprocessing.preprocessor import preprocess_users


def make_users() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "user_id": [1, 2],
            "x_m": [10.0, 20.0],
            "y_m": [30.0, 40.0],
            "z_m": [0.0, 5.0],
            "demand": [1.0, 1.5],
        }
    )


class ValidateUsersTests(unittest.TestCase):
    def test_accepts_valid_data(self) -> None:
        validate_users(make_users())

    def test_rejects_missing_required_column(self) -> None:
        users = make_users().drop(columns="demand")

        with self.assertRaisesRegex(ValueError, "demand"):
            validate_users(users)

    def test_rejects_empty_dataset(self) -> None:
        with self.assertRaisesRegex(ValueError, "không chứa user"):
            validate_users(make_users().iloc[0:0])

    def test_rejects_missing_values(self) -> None:
        users = make_users()
        users.loc[0, "x_m"] = float("nan")

        with self.assertRaisesRegex(ValueError, "giá trị thiếu"):
            validate_users(users)

    def test_rejects_non_finite_numeric_values(self) -> None:
        users = make_users()
        users.loc[0, "z_m"] = float("inf")

        with self.assertRaisesRegex(ValueError, "hữu hạn"):
            validate_users(users)

    def test_rejects_non_numeric_coordinates(self) -> None:
        users = make_users()
        users["x_m"] = users["x_m"].astype(object)
        users.loc[0, "x_m"] = "not-a-number"

        with self.assertRaisesRegex(ValueError, "giá trị số"):
            validate_users(users)


class PreprocessUsersTests(unittest.TestCase):
    def test_removes_duplicate_ids_without_dropping_other_rows(self) -> None:
        users = pd.concat([make_users(), make_users().iloc[[0]]], ignore_index=True)

        processed = preprocess_users(users)

        self.assertEqual(processed["user_id"].tolist(), [1, 2])
        self.assertEqual(len(processed), 2)


if __name__ == "__main__":
    unittest.main()
