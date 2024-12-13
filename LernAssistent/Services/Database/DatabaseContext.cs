// implement the GetUserInfoAsync method to retrieve the user's credit balance from the database.

using Microsoft.EntityFrameworkCore;
using LernAssistent.Entities; // Namespace for the User entity

namespace LernAssistent.Services.Database
{
    public class DatabaseContext : DbContext // DbContext: a part of EF Core. It acts as the bridge between your application and the database. It provides the functionality to query and save data.
    {
        public DbSet<User> Users { get; set; }

        public DatabaseContext(DbContextOptions<DatabaseContext> options) : base(options) { }

        /// <summary>
        /// Retrieves a user's credit balance from the database based on their userId.
        /// </summary>
        /// <param name="userId">The unique identifier of the user.</param>
        /// <returns>A UserInfo object containing the credit balance, or null if the user is not found.</returns>
        public async Task<UserInfo?> GetUserInfoAsync(string userId)
        {
            // Retrieve the user from the database
            var user = await Users.FirstOrDefaultAsync(u => u.UserId == userId);

            if (user == null)
            {
                return null; // User not found
            }

            // Return the user's credit balance wrapped in a UserInfo object
            return new UserInfo { CreditBalance = user.Credits };
        }
    }

    /// <summary>
    /// A DTO to represent user information.
    /// </summary>
    public class UserInfo
    {
        public int CreditBalance { get; set; }
    }
}
