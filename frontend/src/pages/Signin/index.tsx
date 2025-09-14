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
  const { apiError } = useApiError<SigninErrorResponse>(error);
  const { register, handleSubmit, showError, errors } = useSmartForm<SigninValues>({
    initialValues: {
      email: "",
      password: "",
    },
    validate: (values) => {
      const errs: Partial<Record<keyof SigninValues, string>> = {};
      if (!values.email) errs.email = "email is required";
      if (!values.password) errs.password = "password is required";
      return errs;
    },
    onSubmit: async (values) => {
      await signin(values)
    },
  })

  return (
    <div className={styles.container}>
      <form
        className={styles.form}
        onSubmit={handleSubmit}
      >
        <div className={styles.labelContainer}>
          <h5>Sign In</h5>
          <p>Welcome back! Sign into continue</p>
        </div>

        {/* Email */}
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
          {showError("email") && <p className={styles.error}>{errors.email}</p>}
          {apiError && <p className={styles.error}>{apiError.data.email}</p>}
        </div>

        {/* Password */}
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
          {showError("password") && <p className={styles.error}>{errors.password}</p>}
          {apiError && (
            <>
              <p className={styles.error}>{apiError.data.password}</p>
              <p className={styles.error}>{apiError.data.non_field_errors}</p>
              <p className={styles.error}>{apiError.data.detail}</p>
            </>
          )}
        </div>

        {/* Buttons */}
        <div className={styles.wrapper}>
          <Button type="submit" className="btn">
            {isLoading ? <Loader /> : "Sign In"}
          </Button>
        </div>

        <p>Don't have an account? <Link to={"signup"}>Create on now</Link></p>
      </form>
    </div>
  )
}

export default Signin;
