import React, { useEffect } from "react";
import "./VerifyUserAccountPage.css";
import { useParams } from "react-router-dom";
import { useResetOnRouteChange } from "hooks";
import {
  NavLink,
  Button,
  DisplaySuccessDetails,
  DisplayErrorDetails,
  SigninLink,
} from "components";
import {
  useVerifyUserAccountSelector,
  verifyUserAccount,
  resetVerifyUserAccount,
} from "features/auth/verifyUserAccount";
import { triggerToast } from "features/toast";

const VerifyUserAccountPage: React.FC = (): JSX.Element => {
  const { token } = useParams<{ token: string }>();
  const { status, message, errors, data } = useVerifyUserAccountSelector();

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    verifyUserAccount({
      token: token || "",
    });
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
    resetVerifyUserAccount();
  });

  return (
    <div className="grid-12 verify-user-account-page">
      <div className="header">
        <h3 className="form-label">Verify your account</h3>
        <p className="form-description">
          Click the Verify button below to verify your account.
        </p>
      </div>
      <div className="grid-start-2-end-2 content">
        <form className="form" onSubmit={handleSubmit}>
          <DisplayErrorDetails details={errors?.detail} />
          <DisplayErrorDetails details={errors?.token} />
          <DisplayErrorDetails details={errors?.non_field} />
          {data && <DisplaySuccessDetails details={data.detail} />}
          <div className="actions">
            <NavLink
              to="../../"
              type="link"
              className="link back-link"
              icon="arrowBack"
            >
              Back
            </NavLink>
            <Button
              type="submit"
              icon={status === "succeeded" ? "checkCircle" : "click"}
              className="button"
              isLoaderOn={status === "loading"}
              isDisabled={status === "succeeded"}
            >
              Verify
            </Button>
          </div>
          {status === "succeeded" && <SigninLink />}
        </form>
      </div>
    </div>
  );
};

export default VerifyUserAccountPage;
