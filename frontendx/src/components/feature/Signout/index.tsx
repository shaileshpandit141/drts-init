import React, { FC, JSX } from "react";
import { useSignoutMutation } from "features/signout/signoutApi";
import { useAuth } from "features/auth/hooks";

const Signout: FC = (): JSX.Element | null => {
    const [signout, { isLoading }] = useSignoutMutation();
    const { isAuthenticated, refresh_token } = useAuth();

    const handleSignout = async (event: React.MouseEvent<HTMLButtonElement>) => {
        await signout({
            "refresh_token": refresh_token || ""
        })
    }

    if (isAuthenticated) {
        return (
            <button
                onClick={handleSignout}
                disabled={isLoading}
            >Sign out</button>
        )
    }

    return null
}

export default Signout;
