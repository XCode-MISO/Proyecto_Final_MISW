import http from 'k6/http';
import { check } from 'k6';

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
  const res = http.get('https://microservicios-gateway-1qkjvfz9.uc.gateway.dev/api/vendedores', 
  {
    headers: {
      Authorization: "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjY3ZDhjZWU0ZTYwYmYwMzYxNmM1ODg4NTJiMjA5MTZkNjRjMzRmYmEiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQWRtaW4iLCJyb2xlIjoiYWRtaW4iLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vbWlzdy00MzAxLW5hdGl2ZS1jbG91ZC00MzM3MDIiLCJhdWQiOiJtaXN3LTQzMDEtbmF0aXZlLWNsb3VkLTQzMzcwMiIsImF1dGhfdGltZSI6MTc0NzI3ODUzNiwidXNlcl9pZCI6Ilk3UTBQMkVZNjZOSmJ4TUQxMWRneDF1WEFsOTIiLCJzdWIiOiJZN1EwUDJFWTY2TkpieE1EMTFkZ3gxdVhBbDkyIiwiaWF0IjoxNzQ3Mjc4NTM2LCJleHAiOjE3NDcyODIxMzYsImVtYWlsIjoiYWRtaW5AZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImFkbWluQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.DB_yopt0tMg1qpk7zrM9_V0w1LLbJ3ZEDI2xum6NJNcSIG3g4WOvDlFaNczrjG6kaIN0N66ZxblyuxNykQ3Uns_t7VS_A1CkkEpOKoJ033MUzkiIzq0Fc-G678XAelg5quJ08PG5tqP1P4_AqAaMSndG4PIFbnauVweCzrZdvVV9oN1vVAAYjRsyl9_8l9CnSGUmAvyCQ4tWQhLLgrCcgfce8BEeHVm2TUs9e0WvwGd8ubU47i9eG80th0j40rZQ2r83em8s-bK8VTi84tG8hKmgu_Sdng-mFkx5aCr6JKJEDBAzxM6aZTBZ8z82x7xtQjLEfDYFkenX8G6ZVjxdtQ"
    }
  });
  check(res, {
    'is status 200': (r) => r.status === 200,
  });
}