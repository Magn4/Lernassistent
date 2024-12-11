using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.EntityFrameworkCore;
using Lernassistent.src.main.database;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddControllers();
builder.Services.AddHttpClient(); // For communicating with microservices

// Configure PostgreSQL database context
builder.Services.AddDbContext<DatabaseContext>(options =>
    options.UseNpgsql("Host=localhost;Port=5432;Database=ai_project_db;Username=admin;Password=admin_password"));

// Create the application and apply migrations before building
var app = builder.Build();

// Apply any pending migrations
using (var scope = app.Services.CreateScope())
{
    var dbContext = scope.ServiceProvider.GetRequiredService<DatabaseContext>();
    dbContext.Database.Migrate();  // Applies any pending migrations
}

// Configure the HTTP request pipeline
app.MapControllers();  // Register your controller routes

app.Run();
