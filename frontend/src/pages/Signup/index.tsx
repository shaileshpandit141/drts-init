/* eslint-disable react-hooks/exhaustive-deps */
import React, { FC, JSX, useEffect, } from "react";
import styles from "./Signup.module.css";
import Button from "components/ui/Button";
import { useSmartForm } from "hooks/useSmartForm";
import { useSignupMutation } from "features/signup/signupApi";
import { useApiError } from "hooks/useApiError";
import { SigninErrorResponse } from "features/auth/types";
import Loader from "components/ui/Loader";
import Input from "components/ui/Input";
import { Link } from "react-router-dom";
import { useToast } from "features/toast/hooks";

interface SignupValues {
  email: string;
  password: string;
}

const Signup: FC = (): JSX.Element => {
  const [signup, { isLoading, error, data, isSuccess }] = useSignupMutation();
  const { apiError, resetError } = useApiError<SigninErrorResponse>(error);
  const { triggerToast } = useToast();
  const { register, handleSubmit, showError, errors } = useSmartForm<SignupValues>({
    initialValues: {
      email: "",
      password: "",
    },
    validate: (values) => {
      const errs: Partial<Record<keyof SignupValues, string>> = {};
      if (!values.email) errs.email = "email is required";
      if (!values.password) errs.password = "password is required";
      return errs;
    },
    onSubmit: async (values) => {
      await signup(values)
    },
  })

  useEffect(() => {
    if (isSuccess && data) {
      resetError()
      triggerToast("success", data.detail)
    }
  }, [isSuccess, data])

  return (
    <div className={styles.container}>
      <form
        className={styles.form}
        onSubmit={handleSubmit}
      >
        <div className={styles.labelContainer}>
          <h5>Sign Up</h5>
          <p>Sign up to continue</p>
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
          {showError("email") && <p className={styles.error}>{errors.email}</p>}
          {apiError && <p className={styles.error}>{apiError.data.email}</p>}
        </div>

        {/* --- Password --- */}
        <div className={styles.wrapper}>
          <Input
            label={{ left: "password", right: "verify existing account?" }}
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

        {/* --- Success response message --- */}
        {data && (<p className={styles.success}>{data?.detail}</p>)}

        {/* --- Buttons --- */}
        <div className={styles.wrapper}>
          <Button type="submit" className="btn">
            {isLoading ? <Loader /> : "Sign up"}
          </Button>
        </div>

        <p>You have an account? <Link to={"/signin"}>Sign in now</Link></p>
      </form>
    </div>
  )
}

export default Signup;
