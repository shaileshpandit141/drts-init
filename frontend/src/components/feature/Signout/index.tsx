import React, { FC, JSX } from "react";
import { useSignoutMutation } from "features/auth/authApi";
import { useAuth } from "features/auth/hooks";
import IconButton from "components/ui/IconButton";

const Signout: FC = (): JSX.Element | null => {
    const [signout, { isLoading }] = useSignoutMutation();
    const { isAuthenticated, refresh_token } = useAuth();

    const handleSignout = async (event: React.MouseEvent<HTMLButtonElement>) => {
        await signout({
            "refresh_token": refresh_token || ""
        })
    }

    if (!isAuthenticated) {
        return null
    }

    return (
        <IconButton
            onClick={handleSignout}
            disabled={isLoading}
        >Sign out</IconButton>
    )
}

export default Signout;
