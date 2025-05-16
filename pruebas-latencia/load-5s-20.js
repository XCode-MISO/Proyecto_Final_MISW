import http from 'k6/http'
import faker from 'k6/x/faker'
import { check } from 'k6'

import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js'

const startTime = Date.now()
const token =
  '<token>'

const clients = [
  'DFqVO85l7nhV6D6YzX46TVoPryF3',
  'hxzdXrMuc9WndaA8yWqtZzBJsXx1',
  'hv91CdrFXuRB08RMEeSieYKn6OI2',
  '6JUillHYegQKeOkl4ZJEXSLSMA13',
  'Y6K63TNjTUaSo205mZdC8vdVkMW2',
  'nsrN6drZzFS94ySdpxPnaZ68OOM2',
]

const vendedores = [
  '9a04bf1b-fd15-4877-9c46-d6309e1b26fb',
  '0e754fbf-cd63-47bb-a3c5-e4d8e30019cb',
  '9e53eeff-6e0f-4271-b2f5-5054ae93b949',
  'b635b23e-f639-4c93-a13c-b197519958b4',
  '33415345-5899-4005-a743-74d29fb16d8e',
  'df1ec50d-9351-46ca-b1ec-1aac5fb8aa43',
  'c6c4b79b-8aa5-427a-b312-7b52c3c8337e',
  'ef97bfdd-941b-4c18-a6e2-a9732211212f',
  '9f0a611f-13c4-4af4-800f-dd169957330e',
  'a562606d-fcc2-4f39-9a19-d74e1f536a65',
  '3b07a467-b7ae-4c93-90b3-e1ee8f1aa326',
  '9c25cd27-50de-46eb-a573-03dc9841e913',
  '153db5f6-9a81-4bf5-bd14-51e350b9834b',
  'bbc72f49-c70a-4c8a-94d9-4736281514d5',
  '65e41ea3-6ae5-4c62-8526-2c9fec7da683',
  'f12f8ab4-7a8d-424e-8b53-a7b27ca27454',
  'Y7Q0P2EY66NJbxMD11dgx1uXAl92',
  'RAhzXrmKybe3Kq3MI9QxZkpo9Yy2',
  'wXzhGvAMt0M036ye48UzRuDUBKk1',
  'HwMsWLD92vZk4q7X9lVibmH3XRk1',
  'AyZGJG9wTJd6fkNeADpUxvlFO0a2',
  '289af5c8-710d-4d49-ac7d-a837a3a6458a',
  '7b407125-e404-46b9-b13f-cb8091d3af08',
  'f004b479-ff19-4bba-890c-54961f5bd486',
  '87c74936-bde9-4aff-b906-82afe2e2bf44',
  'de21ba80-817f-400b-be11-43e6cec45060',
  '2b6621f7-a0fd-473d-bdd4-cd6f5ec0b785',
  'a77e4e94-5733-487f-b612-cc8ce3ff2b92',
  'b1ae5635-bb35-41a1-8905-a96b5b61c158',
  'fe29d76e-84bf-45ba-bd2d-1656e40c5a6e',
  '4749f730-d184-4e8a-ae29-097e14561a47',
  '497483c1-d810-4256-af06-51c4cad37910',
  '4394fc5c-28ae-4d2e-94ba-d35aa03d0dde',
  'a869da20-c6ac-4509-82eb-87b1095cb81b',
  '03439591-718f-4b91-921b-800bd2445e52',
  '9e2ec0fd-0636-496b-b815-cd90d49b01e0',
  'ebaa9102-2395-4542-86a2-cc81971a3b16',
  '4ef677f5-1180-4eeb-a5bf-3ca8c5357c4c',
]

const addresses = [
  'Calle 123# 1-25, Bogota, Colombia',
  'Calle 26# 33-11, Bogota, Colombia',
  'Avenida 68# 34-45, Bogota, Colombia',
  'Carrera 19# 72-11, Bogota, Colombia',
  'Carrera 15# 34-11, Bogota, Colombia',
  'Calle 85# 11-11, Bogota, Colombia',
  'Calle 45# 56-11, Bogota, Colombia',
  'Avenida 19# 11-45, Bogota, Colombia',
  'Calle 68# 23-11, Bogota, Colombia',
  'Calle 13# 4-11, Bogota, Colombia',
  'Calle 50# 11-11, Bogota, Colombia',
  'Calle 17# 45-11, Bogota, Colombia',
  'Calle 22# 11-11, Bogota, Colombia',
  'Calle 11# 45-11, Bogota, Colombia',
  'Calle 90# 34-11, Bogota, Colombia',
  'Avenida 11# 34-45, Bogota, Colombia',
  'Calle 76# 11-11, Bogota, Colombia',
  'Calle 95# 11-11, Bogota, Colombia',
  'Calle 82# 45-11, Bogota, Colombia',
]

const getRandomAddress = () => {
  return addresses[Math.floor(Math.random() * addresses.length)]
}

const getRandomParada = () => {
  return {
    nombre: faker.person.firstName(),
    fecha: new Date(Date.now() + 60 * 60 * 24).toISOString(),
    cliente: {
      id: clients[Math.random() * clients.length],
      nombre: faker.person.firstName(),
      direccion: getRandomAddress(),
    },
    vendedor: {
      id: vendedores[Math.random() * vendedores.length],
      nombre: faker.person.firstName(),
      direccion: getRandomAddress(),
    },
  }
}

const generateRandomParadaList = (amount) => {
  return new Array(amount).fill(0).map(getRandomParada)
}

export const options = {
  scenarios: {
    constant_arrival: {
      executor: 'constant-arrival-rate',
      duration: '30s', // total duration
      preAllocatedVUs: 150, // to allocate runtime resources

      rate: 20, // number of constant iterations given `timeUnit`
      timeUnit: '1s',
    },
  },
}

export default function () {
  const body = {
    nombre: faker.company.company(),
    inicio: getRandomAddress(),
    fin: getRandomAddress(),
    paradas: generateRandomParadaList(randomIntBetween(2, 5)),
  }
  const res = http.post(
    'https://microservicios-gateway-1qkjvfz9.uc.gateway.dev/api/generate-route',
    JSON.stringify(body),
    {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    }
  )
  check(res, {
    'is status 200': (r) => r.status === 200,
    'is faster than 5s': (r) => r.timings.duration < 5000,
  })
}
