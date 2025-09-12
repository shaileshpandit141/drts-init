import React, { FC, JSX } from "react";
import styles from "./Signin.module.css";
import Button from "components/ui/Button";
import { useSmartForm } from "hooks/useSmartForm";
import { useSigninMutation } from "features/auth/authApi";
import { ErrorResponse } from "features/auth/types";
import { normalizeApiError } from "utils/normalizeApiError";
import Loader from "components/ui/Loader";

interface SigninValues {
  email: string;
  password: string;
}

const Signin: FC = (): JSX.Element => {
  const [signin, { isLoading, error }] = useSigninMutation();
  const errors = normalizeApiError<ErrorResponse>(error);
  const { register, handleSubmit } = useSmartForm<SigninValues>({
    initialValues: {
      email: "",
      password: "",
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
        <input
          type="email"
          placeholder="email"
          className={styles.input}
          required
          {...register("email")}
        />
        {/* {!isLoading && errors && (
          <p className={styles.error}>{errors?.data.email}</p>
        )} */}
        <input
          type="password"
          placeholder="password"
          className={styles.input}
          required
          {...register("password")}
        />
        {/* {!isLoading && errors && (
          <>
            <p className={styles.error}>{errors?.data.password}</p>
            <p className={styles.error}>{errors?.data.non_field_errors}</p>
            <p className={styles.error}>{errors?.data.detail}</p>
          </>
        )} */}
        <div className={styles.actionBtnContiner}>
          <Button className="btn">Sign up</Button>
          <Button className="btn">
            {isLoading ? <Loader /> : "Sign in"}
          </Button>
        </div>
        {errors && (
          <>
            <p className={styles.error}>{errors?.data.email}</p>
            <p className={styles.error}>{errors?.data.password}</p>
            <p className={styles.error}>{errors?.data.non_field_errors}</p>
            <p className={styles.error}>{errors?.data.detail}</p>
          </>
        )}
      </form>
    </div>
  )
}

export default Signin;
