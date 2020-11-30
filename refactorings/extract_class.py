from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from refactorings.gen.Java9_v2Parser import Java9_v2Parser
from refactorings.gen.Java9_v2Listener import Java9_v2Listener


class ExtractClassRefactoringListener(Java9_v2Listener):
    """
        To implement the extract class refactoring
    """

    def __init__(self, common_token_stream: CommonTokenStream = None,
                 class_identifier: str = None):
        """
        :param common_token_stream:
        """
        self.enter_class = False
        self.token_stream = common_token_stream
        self.class_identifier = class_identifier
        # Move all the tokens in the source code in a buffer, token_stream_rewriter.
        if common_token_stream is not None:
            self.token_stream_rewriter = TokenStreamRewriter(common_token_stream)
        else:
            raise TypeError('common_token_stream is None')
        self.field_dict = {}
        self.method_name = []
        self.method_no = 0

        # Exit a parse tree produced by Java9_v2Parser#normalClassDeclaration.

    def enterNormalClassDeclaration(self, ctx: Java9_v2Parser.NormalClassDeclarationContext):
        if ctx.identifier().getText() != self.class_identifier:
            return
        self.enter_class = True

    # Exit a parse tree produced by Java9_v2Parser#normalClassDeclaration.
    def exitNormalClassDeclaration(self, ctx: Java9_v2Parser.NormalClassDeclarationContext):
        self.enter_class = False

    # when exiting from a class attribute (field) declaration this method is invoked.
    # This method adds attributes of the target class to a dictionary
    def enterFieldDeclaration(self, ctx: Java9_v2Parser.FieldDeclarationContext):
        if not self.enter_class:
            return

        field_id = ctx.variableDeclaratorList().variableDeclarator(i=0).variableDeclaratorId().identifier().getText()
        self.field_dict[field_id] = []
        print("field_id is", field_id)
        print("_________________")

    # Enter a parse tree produced by Java9_v2Parser#methodDeclaration.
    def enterMethodDeclaration(self, ctx: Java9_v2Parser.MethodDeclarationContext):
        if not self.enter_class:
            return
        m = []
        m_name = ctx.methodHeader().methodDeclarator().identifier().getText()
        self.method_no = self.method_no + 1
        m.append(m_name)
        m.append(self.method_no)
        self.method_name.append(m)
        print("Method name is:", m_name, " no. = ", self.method_no)
        print("methods are: ", self.method_name)
        print(" MMMMMMMMMMMMMMMMMMMMM ")

    # Exit a parse tree produced by Java9_v2Parser#methodDeclaration.
    def exitMethodDeclaration(self, ctx: Java9_v2Parser.MethodDeclarationContext):
        if not self.enter_class:
            return
        print("fields are", self.field_dict)
        print(ctx.methodBody().getText())

    # Exit a parse tree produced by Java9_v2Parser#identifier.
    def exitIdentifier(self, ctx: Java9_v2Parser.IdentifierContext):
        if not self.enter_class:
            return
        if self.method_no == 0:
            return
        print("--------------identifier in method ---------")
        current_method = self.method_name[-1]
        variable_name = ctx.getText()
        print("variable_name =", variable_name)
        print("current methid name =", current_method)
        print("field dictionary =", self.field_dict)
        if variable_name not in self.field_dict:
            print(" variable not in dictionary")
            return
        if not current_method in self.field_dict[variable_name]:
            self.field_dict[variable_name].append(current_method)
        print("field dictionary =", self.field_dict)
