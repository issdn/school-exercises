using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata;
using housetemps.Models;

namespace housetemps.Data
{
    public partial class InfoDbContext : DbContext
    {
        public InfoDbContext()
        {
        }

        public InfoDbContext(DbContextOptions<InfoDbContext> options)
            : base(options)
        {
        }

        public virtual DbSet<Info> Infos { get; set; } = null!;

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
                optionsBuilder.UseMySql("server=localhost;port=3306;database=temperature;user id=root;password=root", Microsoft.EntityFrameworkCore.ServerVersion.Parse("8.0.31-mysql"));
            }
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.UseCollation("utf8mb4_0900_ai_ci")
                .HasCharSet("utf8mb4");

            modelBuilder.Entity<Info>(entity =>
            {
                entity.ToTable("temperature");

                entity.HasIndex(e => e.Id, "id_UNIQUE")
                    .IsUnique();

                entity.Property(e => e.Id).HasColumnName("id");

                entity.Property(e => e.Humidity).HasColumnName("humidity");

                entity.Property(e => e.Temperature).HasColumnName("temperature");

                entity.Property(e => e.Time)
                    .HasColumnType("timestamp")
                    .HasColumnName("time")
                    .HasDefaultValueSql("CURRENT_TIMESTAMP");
            });

            OnModelCreatingPartial(modelBuilder);
        }

        partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
    }
}
