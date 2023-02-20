FROM node:17.3-alpine

WORKDIR /frontend
COPY package.json .
RUN npm install
RUN npm install react-paypal-button-v2 --legacy-peer-deps

COPY . .

CMD ["npm", "run", "start-watch"]