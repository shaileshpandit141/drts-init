import React, { FC, JSX, } from "react";
import styles from "./Signin.module.css";
import Button from "components/ui/Button";
import { useSmartForm } from "hooks/useSmartForm";
import { useSigninMutation } from "features/auth/authApi";
import { useApiError } from "hooks/useApiError";
import { SigninErrorResponse } from "features/auth/types";
import Loader from "components/ui/Loader";
import Input from "components/ui/Input";
import { Link } from "react-router-dom";

interface SigninValues {
  email: string;
  password: string;
}

const Signin: FC = (): JSX.Element => {
  const [signin, { isLoading, error }] = useSigninMutation();
  const { hasApiError, apiError } = useApiError<SigninErrorResponse>(error);
  const { register, handleSubmit, hasError, errors } = useSmartForm<SigninValues>({
    initialValues: {
      email: "",
      password: "",
    },
    fieldValidators: {
      email(value, values) {
        if (value === "") {
          return "Email is required";
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          return "Invalid email format";
        }
      },
      password(value, values) {
        if (value === "") {
          return "Password is required"
        }
      },
    },
    onSubmit: async (values) => {
      await signin(values)
    },
  })

  return (
    <div className={styles.container}>

      {/* --- Meta data --- */}
      <title>Sign in</title>

      <form
        className={styles.form}
        onSubmit={handleSubmit}
      >

        {/* --- Lables --- */}
        <div className={styles.labelContainer}>
          <h5>Sign In</h5>
          <p>Welcome back! Sign in to continue</p>
        </div>

        {/* --- Email --- */}
        <div className={styles.wrapper}>
          <Input
            label={{ left: "email" }}
            input={{
              type: "email",
              placeholder: "example@gmail.com",
              required: true,
              autoComplete: "off",
              ...register("email")
            }}
          />
          {hasError("email") && <p className={styles.error}>{errors.email}</p>}
          {hasApiError && <p className={styles.error}>{apiError.data.email}</p>}
        </div>

        {/* --- Password --- */}
        <div className={styles.wrapper}>
          <Input
            label={{ left: "password", right: "forgot your password?" }}
            input={{
              type: "password",
              placeholder: "••••••••",
              required: true,
              ...register("password")
            }}
          />
          {hasError("password") && <p className={styles.error}>{errors.password}</p>}
          {hasApiError && (
            <>
              <p className={styles.error}>{apiError.data.password}</p>
              <p className={styles.error}>{apiError.data.non_field_errors}</p>
              <p className={styles.error}>{apiError.data.detail}</p>
            </>
          )}
        </div>

        {/* --- Buttons --- */}
        <div className={styles.wrapper}>
          <Button type="submit" className="btn">
            {isLoading ? <Loader /> : "Sign in"}
          </Button>
        </div>

        <p>Don't have an account? <Link to={"/sign-up"}>Create on now</Link></p>
      </form>
    </div>
  )
}

export default Signin;
