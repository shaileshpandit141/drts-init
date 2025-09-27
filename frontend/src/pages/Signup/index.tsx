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
  const { hasApiError, apiError, resetError } = useApiError<SigninErrorResponse>(error);
  const { triggerToast } = useToast();
  const { register, handleSubmit, hasError, errors } = useSmartForm<SignupValues>({
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
        } else if (value.length < 6) {
          return "Password must be at least 6 characters";
        } else if (value === "password") {
          return "Password should not be 'password'";
        } else if (value === values.email) {
          return "Password should not be the same as email";
        }
      },
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

      {/* --- Meta data --- */}
      <title>Sign up</title>

      <form
        className={styles.form}
        onSubmit={handleSubmit}
      >

        {/* --- Lables --- */}
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
          {hasError("email") && <p className={styles.error}>{errors.email}</p>}
          {hasApiError && <p className={styles.error}>{apiError.data.email}</p>}
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
          {hasError("password") && <p className={styles.error}>{errors.password}</p>}
          {hasApiError && (
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

        <p>You have an account? <Link to={"/sign-in"}>Sign in now</Link></p>
      </form>
    </div>
  )
}

export default Signup;
