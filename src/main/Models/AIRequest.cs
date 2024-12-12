using System;
using Lernassistent.src.main.Models;  // Ensure this matches the namespace where AIRequest is located

namespace Lernassistent.src.main.Models  // Ensure this namespace matches your project's structure
{
    public class AIRequest
    {
        public string? Text { get; set; }  // Example property
        public string? Language { get; set; }  // Example property
    }
}
