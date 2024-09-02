import { useState } from 'react';

interface UseSubmitEntryHook {
    submitEntry: (entry: string) => void;
    loading: boolean;
    error: string | null;
    response: any;  // You can adjust the type based on your expected response structure
}

const useSubmitEntry = (endpoint: string = 'http://127.0.0.1:2000/entries'): UseSubmitEntryHook => {
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [response, setResponse] = useState<any>(null);

    const submitEntry = async (entry: string) => {
        setLoading(true);
        setError(null);
        setResponse(null);

        try {
            const res = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ entry }),
            });

            if (!res.ok) {
                const errorData = await res.json();
                setError(errorData.error || 'Unknown error occurred');
            } else {
                const data = await res.json();
                setResponse(data);
            }
        } catch (err) {
            setError('Network error');
        } finally {
            setLoading(false);
        }
    };

    return { submitEntry, loading, error, response };
};

export default useSubmitEntry;
