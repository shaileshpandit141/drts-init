import React, { useEffect } from "react";
import "./SignupPage.css";
import { AddSEO } from "SEO";
import { useResetOnRouteChange, useFormDataChange, useURLBuilder } from "hooks";
import {
  Input,
  Button,
  DisplayErrorDetails,
  SigninLink,
  DisplaySuccessDetails,
} from "components";
import {
  signupUser,
  resetSignupUser,
  useSignupUserSelector,
} from "features/auth/signup";
import { SignupCredentials } from "services/authServices";
import { triggerToast } from "features/toast";

const SignupPage: React.FC = () => {
  const { status, message, errors, data } = useSignupUserSelector();
  const verification_uri = useURLBuilder({
    path: "auth/verify-user-account",
  });
  const [formData, handleFormDataChange] = useFormDataChange<SignupCredentials>(
    {
      email: "",
      password: "",
      confirm_password: "",
      verification_uri: verification_uri,
    },
  );

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    signupUser(formData);
  };

  useEffect(() => {
    if (message) {
      if (status === "succeeded") {
        triggerToast("success", message);
      } else if (status === "failed") {
        triggerToast("error", message);
      }
    }
  }, [message, status]);

  useResetOnRouteChange(() => {
    resetSignupUser();
  });

  return (
    <div className="grid-12 signup-page">
      <AddSEO
        title="Sign up"
        description="Join us to access exclusive content and features."
        keywords="signup, register, account, join"
      />
      <div className="grid-start-2-end-2 content">
        <div className="header">
          <h3 className="form-label">Sign up</h3>
          <p className="form-description">Join us by creating your account.</p>
        </div>
        <form className="form" onSubmit={handleSubmit}>
          <Input
            name="email"
            type="email"
            value={formData.email}
            onChange={handleFormDataChange}
            isDisabled={status === "loading" || status === "succeeded"}
            errors={errors?.email}
          />
          <Input
            name="password"
            type="password"
            value={formData.password}
            onChange={handleFormDataChange}
            isDisabled={status === "loading" || status === "succeeded"}
            errors={errors?.password}
          />
          <Input
            name="confirm_password"
            type="password"
            value={formData.confirm_password}
            onChange={handleFormDataChange}
            isDisabled={status === "loading" || status === "succeeded"}
            errors={errors?.confirm_password}
          />
          <DisplayErrorDetails details={errors?.detail} />
          <DisplayErrorDetails details={errors?.non_field} />
          {status === "succeeded" && data && (
            <DisplaySuccessDetails details={data.detail} />
          )}
          <div className="actions">
            <SigninLink />
            <Button
              type="submit"
              icon="signup"
              className="button"
              isLoaderOn={status === "loading"}
              isDisabled={status === "succeeded"}
            >
              sign up
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SignupPage;
