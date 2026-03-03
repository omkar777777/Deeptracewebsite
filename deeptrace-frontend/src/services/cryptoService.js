import api from './api';

export const processCrypto = async (algorithm, action, text, key) => {
    return await api.post('/crypto', {
        algorithm,
        action,
        text,
        key
    });
};