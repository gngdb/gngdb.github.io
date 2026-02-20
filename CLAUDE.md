# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static personal website for Gavia Gray, built using the HTML5 UP "Astral" template. The site is a GitHub Pages personal portfolio that includes:

- Main portfolio page (index.html)
- Blog section (blog.html)
- Microblog section (microblog.html) 
- Static assets (CSS, JavaScript, images)

## Architecture

### Frontend Framework
- **Template**: HTML5 UP "Astral" template
- **Styling**: SCSS-based CSS with responsive design
- **JavaScript**: jQuery-based interactive navigation and panel switching
- **Layout**: Single-page application with animated panel transitions

### Key Components

- **Navigation**: Dynamic panel switching using jQuery animations
- **Responsive Design**: Desktop/mobile breakpoints at 737px
- **Asset Structure**: 
  - `/assets/css/` - Compiled CSS and fonts
  - `/assets/js/` - JavaScript libraries and main application logic
  - `/assets/sass/` - SCSS source files
  - `/images/` - Site images and profile photos

### Content Management

- **Microblog Posts**: Manually added to `microblog.html` with structured HTML
- **Blog Posts**: Referenced in `blog.html` index, individual posts likely in separate files
- **Static Content**: All content is hardcoded in HTML files

## Development Workflow

### CSS Development
- Source files are in `/assets/sass/`
- Main stylesheet: `main.scss`
- Includes responsive breakpoints and component styling
- CSS compilation would require a SASS processor

### Content Updates
- **Microblog**: Use the `./post` script to add new posts. Run `python3 post "content"` from the repo root. Supports plain text and HTML in the content string, plus an optional `-i <image_path>` flag for images. It auto-increments the post ID and inserts at the top of microblog.html.
- **Portfolio**: Update content in `index.html`
- **Blog**: Update `blog.html` index and create individual post files

### No Build System
- This is a static site with no package.json or build automation
- CSS compilation from SASS would need to be set up manually if needed
- Assets are served directly without bundling

## File Structure Notes

- Root-level HTML files serve as main pages
- `/post/` directory exists but appears empty (may be for future blog posts)
- All styling follows the HTML5 UP Astral template conventions
- Mobile-first responsive approach with desktop enhancements

## GitHub Pages Deployment

- Repository appears to be configured for GitHub Pages
- CNAME file present for custom domain
- Static files served directly from master branch