from practice.PR1_douban_zufang import html_parser, html_outputer

if __name__ == '__main__':
    result = []
    for i in  range(1,5):
        index=0+25*(i-1)
        new_data= html_parser.blogParser(index)
        result.extend(new_data)
        j=i
        print(j)
    outputer = html_outputer.HtmlOutputer()
    #outputer.collect_data(new_data)
    outputer.output_html(result)
