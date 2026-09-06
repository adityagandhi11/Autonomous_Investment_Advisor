# Investment Advisor Frontend

This project is the frontend application for the Investment Advisor, built using Angular. It connects to a FastAPI backend via REST API.

## Project Structure

```
investment-advisor-frontend
├── src
│   ├── app
│   │   ├── components
│   │   │   └── dashboard
│   │   │       ├── dashboard.component.ts
│   │   │       ├── dashboard.component.html
│   │   │       └── dashboard.component.css
│   │   ├── services
│   │   │   └── api.service.ts
│   │   ├── models
│   │   │   └── index.ts
│   │   ├── app.component.ts
│   │   ├── app.component.html
│   │   ├── app.component.css
│   │   ├── app.config.ts
│   │   └── app.routes.ts
│   ├── environments
│   │   ├── environment.ts
│   │   └── environment.development.ts
│   ├── index.html
│   ├── main.ts
│   └── styles.css
├── angular.json
├── package.json
├── proxy.conf.json
├── tsconfig.json
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd investment-advisor-frontend
   ```

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Configure the proxy:**
   Update `proxy.conf.json` to point to your FastAPI backend.

4. **Run the application:**
   ```
   ng serve --proxy-config proxy.conf.json
   ```

5. **Access the application:**
   Open your browser and navigate to `http://localhost:4200`.

## Usage

This application allows users to interact with the Investment Advisor backend, providing features such as viewing investment data and managing user preferences.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.