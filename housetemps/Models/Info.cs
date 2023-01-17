using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace housetemps.Models
{
    public partial class Info
    {
        public int Id { get; set; }
        [Required]
        public float Temperature { get; set; }
        [Required]
        public float Humidity { get; set; }
        public DateTime? Time { get; set; }
    }
}
