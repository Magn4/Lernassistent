using System;
using Microsoft.EntityFrameworkCore;

namespace Lernassistent.src.test.DatabaseContextTest
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var options = new DbContextOptionsBuilder<DatabaseContext>()
                .UseNpgsql("Host=localhost;Port=5432;Database=learning_assistant_db;Username=magna;Password=password123") // Replace with your credentials
                .Options;

            using (var context = new DatabaseContext(options))
            {
                // Ensure database exists
                context.Database.EnsureCreated();

                // Create a new user
                var newUser = new User { UserId = "testuser", Credits = 100 };
                context.Users.Add(newUser);
                context.SaveChanges();
                Console.WriteLine("User added!");

                // Read the user back
                var user = context.Users.FirstOrDefault(u => u.UserId == "testuser");
                if (user != null)
                {
                    Console.WriteLine($"User found: {user.UserId} with {user.Credits} credits");
                }

                // Update the user's credits
                if (user != null)
                {
                    user.Credits += 50;
                    context.SaveChanges();
                    Console.WriteLine("User updated!");
                }

                // Delete the user
                if (user != null)
                {
                    context.Users.Remove(user);
                    context.SaveChanges();
                    Console.WriteLine("User deleted!");
                }
            }
        }
    }

    public class DatabaseContext : DbContext
    {
        public DbSet<User> Users { get; set; }

        public DatabaseContext(DbContextOptions<DatabaseContext> options) : base(options) { }
    }

    public class User
    {
        public string? UserId { get; set; }
        public int Id { get; set; } // Primary Key
        public int Credits { get; set; }
    }
}
