import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Election = () => {
    const [election, setElection] = useState();
    
    //Need to be fixed
    /* useEffect(() => {
        axios.get('/api/election/status')
            .then(response => {
                if (response.data.status === 'ongoing') {
                    setElection(response.data.election);
                } else {
                    setElection(null);
                }
            })
            .catch(error => {
                console.error('Error fetching election status:', error);
                setElection(null);
            });
    }, []); */

    return (
        <>
            {election ? (
                <p>There is an active election</p>
            ) : (
                <p>There is no active election</p>
            )}
        </>
    );
}

export default Election;
