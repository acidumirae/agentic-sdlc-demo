Create a new ASP.NET Core 10 Solution using Clean/Domain-Driven Design Architecture.
Structure: Create 4 projects: Domain, Application, Infrastructure, and Web (MVC).
Domain: Create a Weather entity/value object and a IWeatherService interface in the Domain layer to define the contract.
Infrastructure: Implement WeatherService in Infrastructure using IHttpClientFactory to fetch current temperature data from a weather API (e.g., OpenWeatherMap). Handle JSON deserialization.
Application: Create a GetWeatherQuery and GetWeatherQueryHandler (using MediatR) to orchestrate the call.
Web: Create a Razor Page or MVC Controller/View to display the temperature, injecting the Application handler.
Config: Use appsettings.json for API keys and endpoint URLs. Use dependency injection throughout.
