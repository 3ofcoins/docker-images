#!/usr/bin/env ruby

require 'fileutils'
require 'json'
require 'find'
require 'optparse'
require 'tmpdir'

options = {
  description: 'built with docker-rebase',
  build: false,
  save_id: nil
}

op = OptionParser.new do |opts|
  opts.banner = "Usage: #{opts.program_name} [OPTIONS] IMAGE PARENT | --build DOCKER_BUILD_ARGS"

  opts.on '-b', '--build', 'Run `docker build` for base image' do |v|
    options[:build] = v
  end

  opts.on '--description=DESCRIPTION', 'Describe the image in container_config' do |v|
    options[:description] = v
  end

  opts.on '--save-id=PATH', 'Save image ID to a file' do |v|
    options[:save_id] = v
  end

  opts.on '-q', '--quiet', 'Be quiet' do |v|
    $quiet = v
  end

  opts.on '-v', '--verbose', 'Verbose output' do |v|
    $verbose = v
  end
end

op.parse!

if options[:build]
  puts "docker build #{ARGV.join(' ')}" if $verbose
  build_lines = []
  IO.popen([
      'docker', 'build',
      ('-q' unless $verbose),
      *ARGV ].compact) do |docker|
    while ln = docker.gets
      ln = ln.strip
      puts ln unless $quiet
      build_lines << ln
    end
  end
  raise "docker build #{ARGV.join(' ')}: #{$?}" unless $?.success?

  base = build_lines.grep(/^Step \d+ : FROM /).first.sub(/^.* FROM /, '')
  final = build_lines.grep(/^Successfully built /).first[19..-1]
else
  unless ARGV.length == 2
    puts op
    exit 1
  end

  final, base = ARGV
end

final_id = `docker inspect --format '{{.id}}' #{final}`.strip
base_id = `docker inspect --format '{{.id}}' #{base}`.strip

puts "Rebasing #{final} (#{final_id}) onto #{base} (#{base_id})"

def sh(command)
  puts command if $verbose
  system command or raise "#{command}: #{$?}"
end

def tar(command)
  _cmd = "tar "
  _cmd << "-v " if $verbose
  _cmd << command
  _cmd
end

Dir.mktmpdir 'docker-rebase' do |workdir|
  Dir.chdir workdir do
    sh "docker save #{final} | #{tar '-x'}"

    meta = Hash[
      Dir['*/json']
        .map { |jf| [ File.basename(File.dirname(jf)), JSON[File.read(jf)] ] }
    ]

    cur = final_id
    seen_base = false
    ancestry = []

    while cur do
      if seen_base || cur == base_id
        cur = meta.delete(cur)['parent']
        seen_base = true
      else
        ancestry << meta.delete(cur)
        cur = ancestry.last['parent']
      end
    end

    FileUtils.mkdir '_destroot'
    ancestry.reverse.each do |stage|
      removals = `tar -C _destroot -xvf #{stage['id']}/layer.tar`
        .lines
        .map(&:strip)
        .select { |path| File.basename(path) =~ /^\.wh\.(?!\.wh\.)/ }
      removals.each do |removal|
        removal = File.join('_destroot', removal)
        to_remove = File.join(
          File.dirname(removal),
          File.basename(removal).sub(/^\.wh\./, ''))
        if File.exist? to_remove
          FileUtils.rm_rf to_remove, verbose: $verbose
          FileUtils.rm_rf removal, verbose: $verbose
        end
      end
    end

    final_size = 0
    Find.find('_destroot') do |path|
      final_size += File.size(path) if File.file?(path)
    end

    # Dir.entries('.') - ['.', '..']
    sh "#{tar '-C _destroot -c .'} > #{final_id}/layer.tar"
    FileUtils.rm_rf '_destroot', verbose: $verbose

    final_meta = ancestry.shift
    ancestry.each do |meta|
      FileUtils.rm_rf meta['id'], verbose: $verbose
    end

    final_meta['Size'] = final_size
    final_meta['parent'] = base_id
    final_meta['container_config']['Cmd'] = [
      '/bin/sh', '-c', "#(nop) #{options[:description]}"
    ]

    File.write("#{final_id}/json", JSON[final_meta])
    sh "docker rmi #{final_id} #{'> /dev/null' unless $verbose}"
    sh "#{tar '-c .'} | docker load"
  end
end

File.write(options[:save_id], final_id) if options[:save_id]
