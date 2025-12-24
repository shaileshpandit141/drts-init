/* eslint-disable @typescript-eslint/no-unused-vars */
import React, { FC, JSX } from "react";
import "./UserProfile.css"
import { Link } from "react-router-dom";
import { useDropdown } from "hooks/useDropdown";
import Signout from "../Signout";
import { useUserQuery } from "features/user/userApi";
import { useAuth } from "features/auth/hooks";

const UserProfile: FC = (): JSX.Element | null => {
  const { buttonRef, contentRef, toggleDropdown } = useDropdown(
    { transform: "scale(1)" },
    { transform: "scale(0.9)" },
  );
  const { data, isSuccess } = useUserQuery();
  const { isAuthenticated } = useAuth();

  function renderImage() {
    if (isSuccess && data && data.picture) {
      return <img src={data.picture} alt="user-picture-image" />;
    }
    return <p className="no-user-image">{data && data.email.slice(0, 1)}</p>;
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="user-profile">
      <button
        className="profile-action-button"
        ref={buttonRef}
        onClick={toggleDropdown}
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
          <div className="links">
            {data && (
              <Link
                to={`http://localhost:8000/admin/`}
                type="link"
                className="edit-profile"
                target="_blank"
              >
                Admin
              </Link>
            )}
            <Signout />
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
