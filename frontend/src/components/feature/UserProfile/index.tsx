/* eslint-disable @typescript-eslint/no-unused-vars */
import React, { useEffect, FC, JSX } from "react";
import "./UserProfile.css";
import { Link } from "react-router-dom";
import { useDropdownMenu } from "hooks/useDropdownMenu";
import { useAuth } from "features/auth/hooks";
import Signout from "../Signout";
import { useUserMutation } from "features/user/userApi";

const UserProfile: FC = (): JSX.Element | null => {
  const { isAuthenticated } = useAuth();
  const { buttonRef, contentRef, toggleDropdownMenu } = useDropdownMenu(
    { transform: "scale(1)" },
    { transform: "scale(0.8)" },
  );
  const [user, { data, error, isLoading, isSuccess }] = useUserMutation();

  useEffect(() => {
    if (isAuthenticated) {
      user();
    }
  }, [isAuthenticated, user]);

  if (!isAuthenticated && !isSuccess) {
    return null;
  }

  function renderImage() {
    if (data && data.picture) {
      return <img src={data.picture} alt="user-picture-image" />;
    }
    return <p className="no-user-image">{data && data.email.slice(0, 1)}</p>;
  }

  return (
    <div className="user-profile">
      <button
        className="button-as-icon profile-action-button"
        ref={buttonRef}
        onClick={toggleDropdownMenu}
      >
        {renderImage()}
      </button>
      <div className="card-container" ref={contentRef}>
        <div className="card-header">
          <Link to="/dashboard" className="dashboard-link">
            <section className="user-profile-image">{renderImage()}</section>
            <section className="user-profile-info">
              <p className="email">{data && data.email}</p>
              <p className="view-settings">view dashboard</p>
            </section>
          </Link>
          <div className="line-break"></div>
          {data && (
            <Link
              to={`http://localhost:8000/admin/`}
              type="link"
              className="edit-profile"
              target="_blank"
            >
              Django Admin
            </Link>
          )}
          <Signout />
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
