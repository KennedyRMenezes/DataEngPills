FROM node:14
WORKDIR /app-node
# ARG funciona so em tempo de build da imagem
ARG PORT_BUILD=6000
#ENV para funcionar no container
ENV PORT=$PORT_BUILD
EXPOSE $PORT_BUILD
#copia tudo do diretorio do host atual para imagem
COPY . .
RUN npm install
ENTRYPOINT npm start