FROM node:18

WORKDIR /app
COPY frontend/ /app

RUN npm install
RUN npm run build

# Use serve to serve static build
RUN npm install -g serve

CMD ["serve", "-s", "build", "-l", "3000"]
