# frozen_string_literal: true

require 'json'
require 'net/http'
require 'uri'

module LLMBridge
  extend self

  SERVER_URL = 'http://127.0.0.1:8000/parse'

  def open_dialog
    prompts = ['명령을 입력하세요 (예: 가로 4m 세로 3m 높이 2.7m 박스 만들어줘)']
    defaults = ['']
    input = UI.inputbox(prompts, defaults, 'LLM Command')
    return unless input

    text = input[0].to_s.strip
    return if text.empty?

    command = request_command(text)
    execute_command(command)
  rescue StandardError => e
    UI.messagebox("오류: #{e.message}")
  end

  def request_command(text)
    uri = URI.parse(SERVER_URL)
    http = Net::HTTP.new(uri.host, uri.port)

    req = Net::HTTP::Post.new(uri.request_uri, { 'Content-Type' => 'application/json' })
    req.body = JSON.dump({ text: text })

    res = http.request(req)
    raise "서버 응답 실패(#{res.code}): #{res.body}" unless res.code.to_i == 200

    parsed = JSON.parse(res.body)
    parsed.fetch('command')
  end

  def execute_command(command)
    model = Sketchup.active_model

    case command['action']
    when 'create_box'
      width = command.fetch('width_mm').to_f.mm
      depth = command.fetch('depth_mm').to_f.mm
      height = command.fetch('height_mm').to_f.mm

      model.start_operation('LLM Create Box', true)
      group = model.active_entities.add_group
      face = group.entities.add_face([0, 0, 0], [width, 0, 0], [width, depth, 0], [0, depth, 0])
      face.pushpull(height)
      model.commit_operation

    when 'move_selection'
      dx = command.fetch('dx_mm').to_f.mm
      dy = command.fetch('dy_mm').to_f.mm
      dz = command.fetch('dz_mm').to_f.mm

      model.start_operation('LLM Move Selection', true)
      tr = Geom::Transformation.translation([dx, dy, dz])
      model.selection.each { |ent| ent.transform!(tr) if ent.respond_to?(:transform!) }
      model.commit_operation

    else
      raise "지원하지 않는 액션: #{command['action']}"
    end
  rescue StandardError
    model.abort_operation
    raise
  end

  unless file_loaded?(__FILE__)
    menu = UI.menu('Extensions').add_submenu('LLM Bridge')
    menu.add_item('Open Command Panel') { open_dialog }
    file_loaded(__FILE__)
  end
end
