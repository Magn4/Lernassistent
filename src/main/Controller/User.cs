public class User
{
    public int Id { get; set; }
    public string? Name { get; set; }
    public int? Credits { get; set; }  // Track how many external AI credits a user has
}
