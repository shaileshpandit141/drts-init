import React, { FC, JSX, } from "react";
import styles from "./Signin.module.css";
import Button from "components/ui/Button";
import { useSmartForm } from "hooks/useSmartForm";
import { useSigninMutation } from "features/auth/authApi";
import { useApiError } from "hooks/useApiError";
import { ErrorResponse } from "features/auth/types";
import Loader from "components/ui/Loader";

interface SigninValues {
  email: string;
  password: string;
}

const Signin: FC = (): JSX.Element => {
  const [signin, { isLoading, error }] = useSigninMutation();
  const { apiError } = useApiError<ErrorResponse>(error);
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
        {apiError && <p className={styles.error}>{apiError.data.email}</p>}
        <input
          type="password"
          placeholder="password"
          className={styles.input}
          required
          {...register("password")}
        />
        {apiError && (
          <>
            <p className={styles.error}>{apiError.data.password}</p>
            <p className={styles.error}>{apiError.data.non_field_errors}</p>
            <p className={styles.error}>{apiError.data.detail}</p>
          </>
        )}
        <div className={styles.actionBtnContiner}>
          <Button type="submit" className="btn">Sign up</Button>
          <Button type="submit" className="btn">
            {isLoading ? <Loader /> : "Sign in"}
          </Button>
        </div>
      </form>
    </div>
  )
}

export default Signin;
