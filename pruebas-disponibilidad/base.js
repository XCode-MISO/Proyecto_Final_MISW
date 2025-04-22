import http from 'k6/http';

export const options = {
  scenarios: {
    constant_arrival: {
      executor: 'constant-arrival-rate',
      duration: '2m', // total duration
      preAllocatedVUs: 150, // to allocate runtime resources

      rate: 20, // number of constant iterations given `timeUnit`
      timeUnit: '1s',
    },
  },
};

export default function () {
  http.get('https://microservicios-gateway-1qkjvfz9.uc.gateway.dev/api/route');
}