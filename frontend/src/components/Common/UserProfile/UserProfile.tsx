import React, { useEffect } from "react";
import "./UserProfile.css";
import { Link } from "react-router-dom";
import { NavLink, SignoutButton } from "components";
import { useDropdownMenu } from "hooks";
import { user, useUserSelector } from "features/user";
import { isUserAuthenticated } from "utils/isUserAuthenticated";
import { getEnv } from "utils/getEnv";

const UserProfile: React.FC = (): JSX.Element | null => {
  const { buttonRef, contentRef, toggleDropdownMenu } = useDropdownMenu(
    { transform: "scale(1)" },
    { transform: "scale(0.8)" },
  );
  const { status, data } = useUserSelector();

  useEffect(() => {
    if (status === "idle" && isUserAuthenticated()) {
      user();
    }
  }, [status]);

  if (!isUserAuthenticated() || status === "failed") {
    return null;
  }

  return (
    <div className="user-profile">
      <button
        className="button-as-icon profile-action-button"
        ref={buttonRef}
        onClick={toggleDropdownMenu}
      >
        {data && <img src={data.picture} alt="user-picture-image" />}
      </button>
      <div className="card-container" ref={contentRef}>
        <div className="card-header">
          <Link to="/dashboard" className="dashboard-link">
            <section className="user-profile-image">
              {data && <img src={data.picture} alt="user-picture-image" />}
            </section>
            <section className="user-profile-info">
              <p className="email">{data && data.email}</p>
              <p className="view-settings">view dashboard</p>
            </section>
          </Link>
          <div className="line-break"></div>
          {data && (
            <NavLink
              to={`${getEnv("BASE_API_URL")}/admin/`}
              type="link"
              className="edit-profile"
              target="_blank"
              icon="supervisorAccountIcon"
            >
              Django Admin
            </NavLink>
          )}
          <SignoutButton />
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
