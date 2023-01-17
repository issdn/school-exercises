using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using housetemps.Data;
using housetemps.Models;

namespace housetemps.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class InfoController : ControllerBase
    {
        private readonly InfoDbContext _context;
        public InfoController(InfoDbContext context)
        {
            _context = context;
        }

        // GET: api/Info
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Info>>> GetInfos(int rows)
        {
          if (_context.Infos == null)
          {
              return NotFound();
          }
            return await _context.Infos.OrderByDescending(t => t.Id).Take(rows).ToListAsync();
        }

        // GET: api/Info/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Info>> GetInfo(int id)
        {
          if (_context.Infos == null)
          {
              return NotFound();
          }
            var info = await _context.Infos.FindAsync(id);

            if (info == null)
            {
                return NotFound();
            }

            return info;
        }

        // PUT: api/Info/5
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutInfo(int id, Info info)
        {
            if (id != info.Id)
            {
                return BadRequest();
            }

            _context.Entry(info).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!InfoExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // POST: api/Info
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<Info>> PostInfo(Info info)
        {
          if (_context.Infos == null)
          {
              return Problem("Entity set 'InfoDbContext.Infos' is null.");
          }
            _context.Infos.Add(info);
            await _context.SaveChangesAsync();
            return CreatedAtAction("GetInfo", new { id = info.Id }, info);
        }

        // DELETE: api/Info/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteInfo(int id)
        {
            if (_context.Infos == null)
            {
                return NotFound();
            }
            var info = await _context.Infos.FindAsync(id);
            if (info == null)
            {
                return NotFound();
            }

            _context.Infos.Remove(info);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool InfoExists(int id)
        {
            return (_context.Infos?.Any(e => e.Id == id)).GetValueOrDefault();
        }
    }
}
