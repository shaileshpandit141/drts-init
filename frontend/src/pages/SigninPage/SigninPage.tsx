import React, { useEffect } from "react";
import "./SigninPage.css";
import { Link, Navigate, useSearchParams } from "react-router-dom";
import { AddSEO } from "SEO";
import { useFormDataChange, useResetOnRouteChange } from "hooks";
import { isUserAuthenticated } from "utils/isUserAuthenticated";
import {
  Input,
  DisplayErrorDetails,
  Button,
  SignupLink,
  GoogleSigninButton,
} from "components";
import {
  signinUser,
  resetSigninUserErrors,
  useSigninUserSelector,
} from "features/auth/signin";
import { SigninCredentials } from "services/authServices";
import { triggerToast } from "features/toast";

const SigninPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const { status, message, errors } = useSigninUserSelector();
  const [formData, handleFormDataChange] = useFormDataChange<SigninCredentials>(
    {
      email: "",
      password: "",
    },
  );

  const redirectTo = searchParams.get("redirect_to");

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    signinUser(formData);
  };

  useEffect(() => {
    if (message) {
      if (status === "succeeded") {
        triggerToast("success", message);
      } else if (status === "failed") {
        triggerToast("error", message);
      }
    }
  }, [status, message]);

  useResetOnRouteChange(() => {
    resetSigninUserErrors();
  });

  if (isUserAuthenticated() || status === "succeeded") {
    return <Navigate to={redirectTo || "/home"} replace />;
  }

  return (
    <div className="grid-12 signin-page">
      <AddSEO
        title="Sign in"
        description="Sign in to access your account and explore our features."
        keywords="signin, login, authentication"
      />
      <div className="grid-start-2-end-2 content">
        <div className="header">
          <h3 className="form-label">Sign in</h3>
          <p className="form-description">
            Sign in with your existing credentials.
          </p>
        </div>
        <form className="form" onSubmit={handleSubmit}>
          <GoogleSigninButton />
          <Input
            name="email"
            type="text"
            value={formData.email}
            onChange={handleFormDataChange}
            isDisabled={status === "loading"}
          />
          <DisplayErrorDetails details={errors?.email} />
          <Input
            name="password"
            type="password"
            value={formData.password}
            onChange={handleFormDataChange}
            isDisabled={status === "loading"}
          />
          <DisplayErrorDetails details={errors?.password} />
          <DisplayErrorDetails details={errors?.non_field} />
          <DisplayErrorDetails details={errors?.detail} />
          <div className="split-container">
            <span></span>
            <Link to="/forgot-password" className="forgot-password-link">
              Forgot password
            </Link>
          </div>
          <div className="actions">
            <SignupLink />
            <Button
              type="submit"
              icon="signin"
              className="button"
              isLoaderOn={status === "loading"}
            >
              sign in
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SigninPage;
