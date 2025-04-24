import http from 'k6/http';
import { check } from 'k6';

export const options = {
  scenarios: {
    constant_arrival: {
      executor: 'constant-arrival-rate',
      duration: '2m', // total duration
      preAllocatedVUs: 150, // to allocate runtime resources

      rate: 7, // number of constant iterations given `timeUnit`
      timeUnit: '1s',
    },
  },
};

export default function () {
  const res = http.get('https://microservicios-gateway-1qkjvfz9.uc.gateway.dev/api/vendedores');
  check(res, {
    'is status 200': (r) => r.status === 200,
  });
}