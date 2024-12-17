using Microsoft.EntityFrameworkCore;

namespace Lernassistent.src.main.database
{
    public class DatabaseContext : DbContext
    {
        public DbSet<User> Users { get; set; }

        public DatabaseContext(DbContextOptions<DatabaseContext> options) : base(options) { }
    }

    public class User
    {
        public string? UserId { get; set; }
        public int Id { get; set; } 
        public int Credits { get; set; }
    }
}
