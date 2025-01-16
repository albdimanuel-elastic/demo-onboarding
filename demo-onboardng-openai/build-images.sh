# Build and push the frontend
docker build --no-cache -t albertodimanuel275/frontend-demo-onboarding:latest -f ./src/frontend/Dockerfile ./src/frontend
docker push albertodimanuel275/frontend-demo-onboarding:latest

# Build and push the backend

docker build --no-cache -t albertodimanuel275/backend-demo-onboarding:latest -f ./src/backend/Dockerfile ./src/backend
docker push albertodimanuel275/backend-demo-onboarding:latest
