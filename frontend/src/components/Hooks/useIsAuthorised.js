import { useEffect, useState } from 'react';

function useIsValidStaff(staffTypes) {
    const [isLoading, setIsLoading] = useState(true);
    const [isAuthorised, setIsAuthorised ] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem('token');
        const userType = localStorage.getItem('user_type');

        if (token && staffTypes.includes(userType)) {
            setIsAuthorised(true);
        } else {
            setIsAuthorised(false);
        }
        setIsLoading(false)
    }, [staffTypes])

    return { isAuthorised, isLoading };
}

export function useIsKitchenStaff() {
    return useIsValidStaff(['KitchenStaff']);
}

export function useIsWaitStaff() {
    return useIsValidStaff(['WaitStaff']);
}

export function useIsManager() {
    return useIsValidStaff(['Manager']);
}

export function useIsStaffMember() {
    return useIsValidStaff(['KitchenStaff', 'WaitStaff', 'Manager']);
}

